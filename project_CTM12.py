# -------------------------------------------------------------------------------
# Author: Jaime Tarapues
# Date: 23-04-2021
# Purpose: Transformacion de coordenadas a CTM12
# Organization: Corantioquia
# contact: jaime.tm8@gmail.com
# How to use:
#  Syntax : python project_CTM12.py dirbase dirout
#  dirbase : folder donde se encuentran los Feature Class 
#  dirout : folder donde se guardaran las salidas porcesadas
#  Example : python D:\CORANTIOQUIA\Scripts\Python_Processing\project_CTM12.py D:\CORANTIOQUIA\DATA\shp D:\CORANTIOQUIA\DATA\out
# -------------------------------------------------------------------------------

# Import system modules
import arcpy
import os, sys

dirbase = sys.argv[1]
dirout = sys.argv[2]

#Syntax
if len(sys.argv) != 3:
    os.system('cls')
    arcpy.AddMessage( "\n Revisar los argumentos")
    sys.exit(1)
    
# Set environment settings
arcpy.env.workspace = dirbase
arcpy.env.overwriteOutput = True

# Set local variables
outWorkspace = dirout

try:
    # Define Inventory file
    if len(arcpy.ListFeatureClasses())>0:
        descfile = os.path.dirname(os.path.realpath(__file__)) + "\\" + "Inventory.txt"
        outFile = open(descfile, "w")
        outFile.write("Feature" + "\t" + "Prj_Old" + "\t" + "Prj_New" +"\n")
        outFile.close()
        
        # Use ListFeatureClasses to generate a list of inputs 
        for infc in arcpy.ListFeatureClasses():
            # Determine if the input has a defined coordinate system, can't project it if it does not
            dsc = arcpy.Describe(infc)

            if dsc.spatialReference.Name == "Unknown":
                arcpy.AddMessage('Indenfinido coordinate system: ' + infc)
            else:
                spatial_ref = arcpy.Describe(infc).spatialReference
                arcpy.AddMessage( "\t -> " + infc +"\t"+ spatial_ref.name+ " ...")

                # Determine the new output feature class path and name
                # outfc = os.path.join(outWorkspace, os.path.splitext(infc)[0]+"_CTM12.shp")
                outfc = os.path.join(outWorkspace, os.path.basename(infc))
                
                # Set output coordinate system
                outCS = arcpy.SpatialReference(os.path.join(os.path.dirname(os.path.realpath(__file__)),"MAGNA-SIRGAS_Origen-Nacional.prj"))

                # run project tool
                arcpy.Project_management(infc, outfc, outCS)

                outFile = open(descfile, "a")
                outFile.write(infc + "\t" + spatial_ref.name + "\t CTM12 \n")
                outFile.close()

                arcpy.AddMessage(  "\t done!\n" )

                # check messages
                # print(arcpy.GetMessages())
        arcpy.AddMessage(  "\n \t Process done!!" )
    else:
        arcpy.AddWarning(  "\n No se encontraron elementos en el folder o geodatabase" )
            
except arcpy.ExecuteError:
    arcpy.GetMessages(2)
    
except Exception as ex:
    arcpy.AddMessage(ex.args[0])


