For 2nd point
Need to link this to main !!! In LIne #74
Sure! Here is an example code to store GPS data using CoreData in an iOS app:

Swift

import CoreData

class GPSData: NSManagedObject {
    @NSManaged var latitude: Double
    @NSManaged var longitude: Double
}

class GPSDataStore {
    private let context: NSManagedObjectContext
    
    init(context: NSManagedObjectContext) {
        self.context = context
    }
    
    func addGPSData(latitude: Double, longitude: Double) {
        let gpsData = GPSData(context: context)
        gpsData.latitude = latitude
        gpsData.longitude = longitude
        saveChanges()
    }
    
    func getAllGPSData() -> [GPSData] {
        let request = NSFetchRequest<NSFetchRequestResult>(entityName: "GPSData")
        let sortDescriptor = NSSortDescriptor(key: "latitude", ascending: true)
        request.sortDescriptors = [sortDescriptor]
        
        do {
            let result = try context.fetch(request)
            return result as! [GPSData]
        } catch let error {
            print("Error fetching GPS data: \(error)")
            return []
        }
    }
    
    private func saveChanges() {
        do {
            try context.save()
        } catch let error {
            print("Error saving GPS data: \(error)")
        }
    }
}

To use this code, you need to set up a CoreData stack in your app. Here's an example of how to do that:

import CoreData

class CoreDataStack {
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "GPSDataModel")
        container.loadPersistentStores(completionHandler: { (storeDescription, error) in
            if let error = error as NSError? {
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        })
        return container
    }()
    
    var context: NSManagedObjectContext {
        return persistentContainer.viewContext
    }
}

In this example, "GPSDataModel" is the name of the data model file you created in Xcode. 
To add GPS data to the store, 
you can use the addGPSData(latitude:longitude:) method of the GPSDataStore class. 
To retrieve all GPS data, you can use the getAllGPSData() method.