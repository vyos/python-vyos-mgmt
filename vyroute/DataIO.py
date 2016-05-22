# author=hochikong
import shelve


class IO(object):

    def post(self):
        pass

    def put(self):
        pass


class RawIO(IO):
    # The router node record is in a python shelve object (.dat file).
    def __init__(self, datafile):
        """Initial member self.file.

        :param datafile: a string
        """
        self.file = datafile

    def post(self, key, data):
        """Create a new record in the shelve object.

        :param key: a string
        :param data: a python dictionary
        :return : a python dictionary
        """
        temp = shelve.open(self.file)
        temp[key] = data
        temp.close()
        return {"Result": "Create successfully."}

    def put(self, key, data):
        """Update a record or delete a existing record.

        :param key: a string
        :param data: a python dictionary
        :return: different python dictionaries
        """
        if data == {"content": "delete"}:
            temp = shelve.open(self.file)
            try:
                del temp[key]
                return {"Result": "Delete successfully."}
            except KeyError:
                return {"Result": "There is no key '%s'." % key}
            finally:
                temp.close()
        else:
            self.post(key, data)
            return {"Result": "Update successfully."}

    def get(self, key="all"):
        """Query a specific record or all records.

        :param key: 'none' or a vaild key
        :param args: 'all' or 'none'
        :return: different python dictionaries
        """
        temp = shelve.open(self.file)
        if key == "all":
            print temp
            temp.close()
        else:
            try:
                print temp[key]
            except KeyError:
                return {"Result": "'There is no key '%s'." % key}
            finally:
                temp.close()









