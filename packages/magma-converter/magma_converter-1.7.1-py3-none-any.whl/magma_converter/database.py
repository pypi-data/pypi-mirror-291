from playhouse.migrate import *
from typing import Any, List, Self
import os
import datetime


def database(db_name: str = 'magma.db') -> str:
    """Database location

    Args:
        db_name: database name. Default magma.db

    Returns:
        str: Database location
    """
    user_dir: str = os.path.expanduser('~')
    magma_user_dir: str = os.path.join(user_dir, '.magma')
    os.makedirs(magma_user_dir, exist_ok=True)
    return os.path.join(magma_user_dir, db_name)


db = SqliteDatabase(database(), pragmas={
    'foreign_keys': 1,
    'journal_mode': 'wal',
    'cache_size': -32 * 1000
})


def reset() -> bool | None:
    """Reset database.

    Returns:
        True | None
    """
    database_location = database()
    if os.path.exists(database_location):
        os.remove(database_location)
        db.connect(reuse_if_open=True)
        db.create_tables([Station, Sds])
        db.close()
        print(f"⌛ Reset database: {database_location}")
        return True
    return None


class MagmaBaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(tz=datetime.timezone.utc))

    class Meta:
        database = db


class Station(MagmaBaseModel):
    nslc = CharField(index=True, unique=True, max_length=14)
    network = CharField(index=True)
    station = CharField(index=True)
    channel = CharField(index=True)
    location = CharField()

    class Meta:
        table_name = 'stations'


class Sds(MagmaBaseModel):
    nslc = ForeignKeyField(Station, field='nslc', backref='sds')
    date = DateField(index=True)
    start_time = DateTimeField(index=True, null=True)
    end_time = DateTimeField(index=True, null=True)
    completeness = FloatField()
    sampling_rate = FloatField()
    file_location = CharField()
    file_size = BigIntegerField()

    class Meta:
        table_name = 'sds'
        indexes = (
            (('nslc', 'date'), True),
        )


class DatabaseConverter:
    def __init__(self, sds_results: List[dict[str, Any]]):
        """
        sds_results: SDS success results
            examples:
            {'trace_id': 'VG.INFR.00.EHZ',
              'date': '2018-01-01',
              'start_time': '2018-01-01 00:00:00',
              'end_time': '2018-01-01 23:59:59',
              'sampling_rate': 100.0,
              'completeness': 99.99770833333334,
              'file_location': 'L:\\converted\\SDS\\2018\\VG\\INFR\\EHZ.D\\VG.INFR.00.EHZ.D.2018.001',
              'file_size': 1024, # In byte
              }

        Args:
            sds_results: SDS success results. Can be accessed through SDS `results` property
        """
        self.sds_results = sds_results
        self.station_ids: List[int] = []
        self.sds_ids: List[int] = []

    @property
    def stations(self) -> List[dict[str, Any]]:
        _nslc: List[str] = []
        _stations: List[dict[str, Any]] = []

        for result in self.sds_results:
            nslc = result['trace_id']

            if nslc not in _nslc:
                network, station, channel, location = nslc.split('.')
                __stations: dict[str, Any] = {'nslc': result['trace_id'], 'network': network, 'station': station,
                                              'channel': channel, 'location': location}
                _nslc.append(nslc)
                _stations.append(__stations)

        return _stations

    @property
    def sds(self) -> List[dict[str, Any]]:
        _sds: List[dict[str, Any]] = []

        for result in self.sds_results:
            __sds: dict[str, Any] = {'nslc': result['trace_id'], 'date': result['date'],
                                     'start_time': result['start_time'], 'end_time': result['end_time'],
                                     'completeness': result['completeness'], 'sampling_rate': result['sampling_rate'],
                                     'file_location': result['file_location'], 'file_size': result['file_size']}
            _sds.append(__sds)

        return _sds

    @staticmethod
    def update_station(station: dict[str, Any]) -> int:
        """Update stations table

        Args:
            station (dict[str, Any]): Station data

        Returns:
            int: id of the updated station
        """
        _station, created = Station.get_or_create(**station)

        station_id = _station.get_id()

        if created is True:
            return station_id

        _station.nslc = station['nslc']
        _station.network = station['network']
        _station.station = station['station']
        _station.location = station['location']
        _station.channel = station['channel']
        _station.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        _station.save()

        return station_id

    @staticmethod
    def update_sds(sds: dict[str, Any]) -> int:
        """Update sds table.

        Args:
            sds: SDS success results. Can be accessed through SDS `results` property

        Returns:
            int: id of sds model
        """
        _sds, created = Sds.get_or_create(
            nslc=sds['nslc'],
            date=sds['date'],
            defaults={
                'start_time': sds['start_time'],
                'end_time': sds['end_time'],
                'sampling_rate': sds['sampling_rate'],
                'completeness': sds['completeness'],
                'file_location': sds['file_location'],
                'file_size': sds['file_size'],
                'created_at': datetime.datetime.now(tz=datetime.timezone.utc),
            }
        )

        sds_id = _sds.get_id()

        if created is True:
            return sds_id

        _sds.nslc = sds['nslc']
        _sds.date = sds['date']
        _sds.start_time = sds['start_time']
        _sds.end_time = sds['end_time']
        _sds.completeness = sds['completeness']
        _sds.sampling_rate = sds['sampling_rate']
        _sds.file_location = sds['file_location']
        _sds.file_size = sds['file_size']
        _sds.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        _sds.save()

        return sds_id

    def update(self) -> Self:
        """
        Bulk update:
        https://docs.peewee-orm.com/en/latest/peewee/querying.html#bulk-inserts

        Upsert:
        https://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert

        Returns:
            Self
        """
        for station in self.stations:
            station_id: int = self.update_station(station)
            if station_id not in self.station_ids:
                self.station_ids.append(station_id)

        for sds in self.sds:
            sds_id: int = self.update_sds(sds)
            if sds_id not in self.sds_ids:
                self.sds_ids.append(sds_id)

        return self
