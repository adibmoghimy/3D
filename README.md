# 3D
Gaply Event
1. The first dwg file must converted to a dxf file. 
2. The generated dxf file can be read in two ways in python. 
  - by ezdxf library (plans.py)
  - by comtypes.client (Load.py): here the AutoCAD app must run
3. Entities are separated according to their spatial position. Here, I used the DBSCAN algorithm. I think this is not a good idea to use this algorithm. My idea
was to use OpenCV library. First, we create an image file from the dwg file (png, jpeg, ...). Then, OpenCV or pre-trained models can detect plans and elevations. 
The problem is how we can map the generated image into the original dwg file. I found this solution, but there was no time to apply it. When we load the dxf file in Python,
We loop in the entities and select the ones that have the lowest and highest x and y values. After that, we subtract the highest and lowest x and y values from each other:
(max(x) - min(x), max(y) - min(y). In this way, we have a scale.
4. After separating plans, we must separate plans and elevations. Pretrained models can do this perfectly with low error. I tested this by bing and it works perfectly.
I think the dalle api (open ai) can handle this part. Its api was not free and I can't work on this part. Also, it can predict each elevation belongs to which side (west side, east side, ...).
5. The plans and elevations must map to each other to prepare for the 3D rendering. We can create an excel file with multiple sheets. Each sheet belongs to each plan or
elevation. Inside it sheet, the coordinates of that plan or elevation existed. We can send this CSV file to chatgpt4 to analyze them. 
