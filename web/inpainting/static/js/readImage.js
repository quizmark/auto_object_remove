var fileTag = document.getElementById("filetag"),
    preview = document.getElementById("preview"),
    ctx = preview.getContext('2d');
var check_img=false;
var reader;  
var img;
fileTag.addEventListener("change", function() {
  check_img=false;
  changeImage(this);
  alert("uploaded");
});

function changeImage(input) {
  if (input.files && input.files[0]) {
    reader = new FileReader();
   
    reader.onload = function(e) {
        img = new Image();
        img.onload = function(){
          // preview.width = 500;
          // preview.height = 500;
          ctx.drawImage(img,0,0,500,500);
        }
        img.src = e.target.result;
        //preview.setAttribute('src', e.target.result);
        check_img=true;
    }
    reader.readAsDataURL(input.files[0]);
  }
}

function Inpaint(input,selection){
  if(selection==1)
  {
    $.ajax({type: 'POST',
      url: 'process-image/',
      data: {csrfmiddlewaretoken: "{{ csrf_token }}",file:input,selection:"1"},
      success:  function(response){
        alert("1");
        var result= document.getElementById("result");
        result.src=response;
      },
    });
  }
  if(selection==2)
  {
    t=[]
    for(var x in  boundingBoxes)
    {
      t.push(boundingBoxes[x].x+"_"+boundingBoxes[x].y+"_"
        +boundingBoxes[x].w+"_"+boundingBoxes[x].h);
    }
    $.ajax({type: 'POST',
      url: 'hprocess-image/',
      data: {csrfmiddlewaretoken: "{{ csrf_token }}",file:input,selection:"2",'arr':t},
      success:  function(response){
        //alert(response);
        alert("2");
        var result= document.getElementById("result");
        result.src=response;
      },
    });
  }
}

function processImage(){
  if(check_img==true){
    $.ajax({type: 'POST',
      url: 'upload-image/',
      data: {csrfmiddlewaretoken: "{{ csrf_token }}",preview:reader.result},
      success:  function(response){alert("server saved img ");Inpaint(response,1);},
    });
  }
  else{
    alert("Image Not Found!");
  }
}

function processImage2(){
  if(check_img==true){
    $.ajax({type: 'POST',
      url: 'upload-image/',
      data: {csrfmiddlewaretoken: "{{ csrf_token }}",preview:reader.result},
      success:  function(response){alert("server saved img ");Inpaint(response,2);},
    });
  }
  else{
    alert("Image Not Found!");
  }
}

const annotation = {
  x: 0,
  y: 0,
  w: 0,
  h: 0,
  printCoordinates: function () {
    console.log('X: ${this.x}px, Y: ${this.y}px, Width: ${this.w}px, Height: ${this.h}px');
  }
};
let boundingBoxes = [];
// the actual rectangle, the one that is being drawn
let o={};
let m = {},
// a variable to store the point where you begin to draw the rectangle    
start = {};
// a boolean 
let isDrawing = false;

function handleMouseDown(e) {
  start = oMousePos(preview, e);
  isDrawing = true; 
  //console.log(start.x, start.y);
  preview.style.cursor = "crosshair";
}

function handleMouseMove(e) { 
    if(isDrawing){
    m = oMousePos(preview, e);
    ctx.clearRect(0, 0, preview.width, preview.height);
    ctx.drawImage(img,0,0,500,500);
    //changeImage(fileTag);
    draw();
    }
}

function handleMouseUp(e) { 
    preview.style.cursor = "default";
    isDrawing = false;

    const box = Object.create(annotation);
    box.x = o.x;
    box.y = o.y;
    box.w = o.w;
    box.h = o.h;

    boundingBoxes.push(box);
    draw();
    box.printCoordinates();
    console.log(boundingBoxes)
    }

function draw() {  
    o.x = start.x;  // start position of x
    o.y = start.y;  // start position of y
    o.w = m.x - start.x;  // width
    o.h = m.y - start.y;  // height

    //clearcanvas();
    //ctx.clearRect(0, 0, preview.width, preview.height);//////***********
    // draw all the rectangles saved in the rectsRy
    boundingBoxes.map(r => {drawRect(r)})
    // draw the actual rectangle
    drawRect(o);  
}

preview.addEventListener("mousedown", handleMouseDown);

preview.addEventListener("mousemove", handleMouseMove);

preview.addEventListener("mouseup", handleMouseUp);

function savecanvas(){
    //ctx.clearRect(0, 0, preview.width, preview.height);
    var savedBoxes = boundingBoxes.slice(0);
    console.log(savedBoxes); // ok
    }

function resetcanvas(){
    //ctx.clearRect(0, 0, preview.width, preview.height);
    boundingBoxes.length = 0;
    console.log(boundingBoxes); // ok
    }

function drawRect(o){
        ctx.strokeStyle = "limegreen";
        ctx.lineWidth = 2;
        ctx.beginPath(o);
        ctx.rect(o.x,o.y,o.w,o.h);
        ctx.stroke();
    }

// Function to detect the mouse position

function oMousePos(preview, evt) {
  let ClientRect = preview.getBoundingClientRect();
    return { 
    x: Math.round(evt.clientX - ClientRect.left),
    y: Math.round(evt.clientY - ClientRect.top)
  }
}