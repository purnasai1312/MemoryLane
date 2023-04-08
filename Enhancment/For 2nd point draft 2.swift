For 2nd point draft 2

import CoreData

# Define the Core Data stack
class CoreDataStack:
    def __init__(self):
        # Initialize the managed object model
        self.managedObjectModel = NSManagedObjectModel.mergedModel(from: [Bundle.main])!

        # Initialize the persistent store coordinator
        let persistentStoreCoordinator = NSPersistentStoreCoordinator(managedObjectModel: self.managedObjectModel)
        let fileManager = FileManager.default
        let documentsURL = fileManager.urls(for: .documentDirectory, in: .userDomainMask).last!
        let storeURL = documentsURL.appendingPathComponent("GPSData.sqlite")
        let options = [NSMigratePersistentStoresAutomaticallyOption: true, NSInferMappingModelAutomaticallyOption: true]

        do {
            try persistentStoreCoordinator.addPersistentStore(ofType: NSSQLiteStoreType, configurationName: nil, at: storeURL, options: options)
        } catch {
            fatalError("Failed to initialize the persistent store coordinator: \(error)")
        }

        # Initialize the managed object context
        self.managedObjectContext = NSManagedObjectContext(concurrencyType: .mainQueueConcurrencyType)
        self.managedObjectContext.persistentStoreCoordinator = persistentStoreCoordinator

    # Define the Core Data entities
    class GPSData: NSManagedObject:
        @NSManaged var latitude: Double
        @NSManaged var longitude: Double
        @NSManaged var timestamp: Date

    # Define the functions for working with Core Data
    def save_gps_data(latitude, longitude):
        # Create a new GPSData managed object
        gpsData = GPSData(context: CoreDataStack.managedObjectContext)
        gpsData.latitude = latitude
        gpsData.longitude = longitude
        gpsData.timestamp = Date()
        # Save the managed object context
        try CoreDataStack.managedObjectContext.save()
    
    def get_gps_data():
        # Create a fetch request for the GPSData entity
        fetchRequest = NSFetchRequest<NSFetchRequestResult>(entityName: "GPSData")
        # Execute the fetch request and return the results
        return try CoreDataStack.managedObjectContext.fetch(fetchRequest) as! [GPSData]

Note:
In this code, we define a CoreDataStack class that handles setting up the Core Data stack and provides functions for working with the GPSData entity. We also define the GPSData entity as a subclass of NSManagedObject, which allows us to work with GPS data as managed objects in our Core Data context.

The save_gps_data function creates a new GPSData managed object and sets its properties to the latitude and longitude values passed in. It then saves the managed object context to persist the data to the database.

The get_gps_data function creates a fetch request for the GPSData entity and returns the results as an array of GPSData objects.

Note that this code assumes that you have already set up a Core Data data model with a GPSData entity and generated the corresponding classes using Xcode's code generation feature.