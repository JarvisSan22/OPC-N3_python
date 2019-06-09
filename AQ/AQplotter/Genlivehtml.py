# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:34:24 2019

@author: Jarvis
Createthe live dash HDML
"""

def genLivedash(locname,filename,cols):
    rows="""
    
    """
    
    #generate columns buttons 
    
    for col in cols:
        row='<a href=" '+filename+'-'+col+'.html" target="plot"><button type="button" >'+col+'</button></a>'
        rows=rows+row
    print(rows)
    
    #add rows and avariabls into html 
    
    html="""
    <html>
<style>
.btn-group button {
  background-color: #e6e6fa; /* background */
  border: 1px solid blue; /*  border */
  color: blue; /* blue text */
  padding: 10px 30px; /* Some padding */
  cursor: pointer; /* Pointer/hand icon */
  width: 100%; /* Set a width if needed */
  display: block; /* Make the buttons appear below each other */
}

.btn-group button:not(:last-child) {
  border-bottom: none; /* Prevent double borders */
}


.col{
  float: left;
}
.col + .col{
  float: left;
  margin-left: 20px;
}

/* or */

.col:not(:nth-child(1)){
  float:left;
  margin-left: 20px;
}


</style>
<body style="background-color:#f0f8ff;">


<div class="row">
	<!------Buttons---------------->
	<div class="col"><div class="btn-group">
	<br>
	</br>
	<br>
	</br>
		
		<button>Variables</button>
		"""+rows+"""
		</div>
	</div>
	<!--------Plot target------------>
	<div class="col">
	<iframe src= '"""+filename+"""-pm2.5.html' name="plot" width="1000pt" height="700pt" frameBorder="0" ></iframe>
	</div>
</div> 
</body>
</html>
    
    
    
    """
    print("Generate Dashboard")
    pagename="Plots//"+locname+filename+".html"
    file = open(pagename,"w+") #open file in binary mode
    file.writelines(html)
    file.close()
    
