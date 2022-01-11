name := "TestProject"

version := "0.1"

scalaVersion := "2.13.3"

val sparkVersion = "2.0.0"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % sparkVersion
)
