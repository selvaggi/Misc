import csv
from collections import OrderedDict

class DataSets(object):
    #_______________________________________________________________________________
    def __init__(self, confirmed_data, recovered_data, deaths_data):

        self.datasets = []
        self.countryDict = dict()
        self.ndata = 999.

        ### start with confirmed
        with open(confirmed_data) as csvfile:
            ## skip header
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            id = 0
            for data in reader:
                dataset = DataSet(id, data[0],data[1],data[2],data[3])
                for k in range(4, len(data)):
                    dataset.fill_ct(k-4, data[k])
                self.ndata = len(dataset.C)
                self.datasets.append(dataset)
                id += 1

        ###  with recovered_data
        with open(recovered_data) as csvfile:
            ## skip header
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for data in reader:
                country = data[1]
                region = data[0]
                for dataset in self.datasets:
                    #print 'country: ', dataset.country, 'region: ', dataset.region
                    if dataset.country == country and dataset.region == region:
                        #print 'HERE'
                        for k in range(4, len(data)):
                            dataset.fill_rt(k-4, float(data[k]))

        ###  with deaths_data
        with open(deaths_data) as csvfile:
            ## skip header
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for data in reader:
                country = data[1]
                region = data[0]
                for dataset in self.datasets:
                    #print 'country: ', dataset.country, 'region: ', dataset.region
                    if dataset.country == country and dataset.region == region:
                        #print 'HERE'
                        for k in range(4, len(data)):
                            dataset.fill_dt(k-4, float(data[k]))

        ### recompute infected
        for ds in self.datasets:
            ds.fill_it()

        ### merge for each country and create dictionary for easier use
        i=0
        for ds in self.datasets:
            uniqueId = ds.id
            country  = ds.country
            i+=1
            j=0
            for ds2 in self.datasets:
                if j>i:
                    if ds2.id == uniqueId:
                        continue
                    elif ds2.country == country:
                        ds.add(ds2)
                j+=1

            self.countryDict[country] = ds


        ## create World/NotChina country
        notchina = DataSet(888, 'world','NotChina',0,0)
        notchina.clear(self.ndata)
        world = DataSet(999, 'world','World',0,0)
        world.clear(self.ndata)

        for ds in self.datasets:
            world.add(ds)
            if ds.country != 'Mainland China':
                notchina.add(ds)

        self.countryDict['NotChina'] = notchina
        self.countryDict['World'] = world

        '''
        for ds in self.datasets:
            print 'id: ', ds.id, 'country: ', ds.country, 'region: ', ds.region, len(ds.C), len(ds.R), len(ds.D), len(ds.I)

        print '-----------------'


        n=0
        for country, ds in self.countryDict.iteritems():
            n += 1
            print 'n: ', n, 'country: ', country, len(ds.C), len(ds.R), len(ds.D), len(ds.I)
        '''
#_______________________________________________________________________________
class DataSet(object):
    def __init__(self, id, region, country, latitude, longitude):
        self.id = id
        self.country = country
        self.region = region
        self.latitude = latitude
        self.longitude = longitude
        self.C = OrderedDict()
        self.R = OrderedDict()
        self.D = OrderedDict()
        self.I = OrderedDict()

    def fill_ct(self, t, c_t):
        self.C[t]=float(c_t)

    def fill_rt(self, t, r_t):
        self.R[t]=float(r_t)

    def fill_dt(self, t, d_t):
        self.D[t]=float(d_t)

    def fill_it(self):
        for t in self.C.keys():
            self.I[t]= self.C[t]-self.R[t]-self.D[t]

    def clear(self, ndata):
        for t in range(ndata):
            self.I[t]=0.
            self.D[t]=0.
            self.R[t]=0.
            self.C[t]=0.

    def getI(self):
        return self.I

    def getC(self):
        return self.C

    def getD(self):
        return self.D

    def getR(self):
        return self.R

    def add(self, dataset):
        for t in self.C.keys():
            self.C[t] += dataset.C[t]
            self.R[t] += dataset.R[t]
            self.D[t] += dataset.D[t]
            self.I[t] += dataset.I[t]

    def resize(self, tmin, tmax):
        Cnew = OrderedDict()
        Rnew = OrderedDict()
        Inew = OrderedDict()
        Dnew = OrderedDict()

        for t in range(len(self.C)):
            if t < tmin or t > tmax:
                del self.C[t]
                del self.R[t]
                del self.I[t]
                del self.D[t]

        for t in range(len(self.C)):
            Cnew[t]=self.C[t+tmin]
            Dnew[t]=self.D[t+tmin]
            Rnew[t]=self.R[t+tmin]
            Inew[t]=self.I[t+tmin]

        self.C=Cnew
        self.R=Rnew
        self.D=Dnew
        self.I=Inew

    def rescaleI(self, scale):
        for t in range(len(self.I)):
            self.I[t]*= scale



#_______________________________________________________________________________

## works on my custom csv
def fill_data_dict(data_dict, csv_file):
    import csv
    with open(csv_file) as csvfile:
         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
         for row in reader:
             #print(', '.join(row))
             #print row
             data_dict[int(row[0])] = float(row[1])


#_______________________________________________________________________________
def fill_jhudata_dict(data_dict, csv_file):
    with open(csv_file) as csvfile:
         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
         for row in reader:
             #print(', '.join(row))
             print row
             #data_dict[int(row[0])] = float(row[1])
