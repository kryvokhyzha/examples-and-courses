package labs

object Lab5 {

def main(args: Array[String]) = {
val sc = new SparkContext(new SparkConf().
  setAppName("lab5"))

val trips = sc.textFile("data/trips/*")
val stations = sc.textFile("data/stations/*")

trips.count()
stations.count()

println("Press [Enter] to quit")
Console.readLine()

sc.stop
}
}
