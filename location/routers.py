class LocationRouter(object):

    def db_for_read(self, model, **hints):
        """
        Attempts to read location models go to sim.
        """
        if model._meta.app_label == 'location':
            return 'sim'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write location models go to sim.
        """
        if model._meta.app_label == 'location':
            return 'sim'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the location app is involved.
        """
        if obj1._meta.app_label == 'location' or \
           obj2._meta.app_label == 'location':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the location app only appears in the 'sim'
        database.
        """
        if app_label == 'location':
            return db == 'sim'
        return None