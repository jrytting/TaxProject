class WriteToFile:
    filename = ""

    def openFile(filename, openFor):
        filename = open(filename, openFor)
        return filename

    def writeToFile(dataToWrite):
        filename.write(dataToWrite)

    def closeFile():
        filename.close