
// 投稿ページ

function entryPostPage(){

    postButton = document.getElementById("post-button");
    postButton.addEventListener("click", submitResizeFile);
    console.log("aaaaa");

    document.addEventListener("DOMContentLoaded", function() {
        canvas = document.getElementById("thumbnail");
        context = canvas.getContext("2d");
    
        //scaleSlider = document.getElementById("scale");
        //scaleValue = document.getElementById("scale-value");
    
        messageArea = document.getElementById("message");
    
        //scaleSlider.addEventListener("change", changeScale);
    
        setFileEventListenner();
    });


    var image = null;
    var fixFileObject = null;
    var scale = null;
    var messageArea = null;



function setFileEventListenner() {
    document.getElementById("id_file").addEventListener("change", createPreview);
}

function createPreview(event) {

    fixFileObject = null;

    var fileObject = event.target.files[0];

    if (typeof fileObject === "undefined") {
        return;
    }

    if (fileObject.type.match(/^image\/(jpeg|png)$/) === null) {
        // jpegとpng以外の場合はクリアして終了
        var fileArea = document.getElementById("file-input");
        fileArea.innerHTML = fileArea.innerHTML;
        setFileEventListenner();
        return;
    }

    fixFileObject = fileObject;

    image = new Image();

    var reader = new FileReader();

    reader.onload = (function(fileObject) {
        return function(event) {
            image.src = event.target.result;// base64
        };
    })(fileObject);

     image.onload = function() {
         drawCanvas();
     }

    reader.readAsDataURL(fileObject);
}

//サムネイルのscaleを決める関数
function setScale(widthScale, heightScale){
    if(widthScale > heightScale){
        scale = heightScale;
    } else{
        scale = widthScale;
    }
}

//scaleを元に、画像のサイズを縮小する関数
function resizeImage(scale){
    if (image !== null) {
        var imageWidth = parseInt(image.width * scale, 10);
        var imageHeight = parseInt(image.height * scale, 10);
        canvas.width = imageWidth;
        canvas.height = imageHeight;
        context.clearRect(0, 0, imageWidth, imageHeight);
        context.drawImage(image, 0, 0, imageWidth, imageHeight);
        }

}


function drawCanvas() {
    if(window.matchMedia( "(max-width: 576px)" ).matches){
        setScale(512 / image.width, 512 / image.height);
        
        //ここも関数にできるよね
        if (image !== null) {
            var imageWidth = parseInt(image.width * scale, 10);
            var imageHeight = parseInt(image.height * scale, 10);
            canvas.width = imageWidth;
            canvas.height = imageHeight;
            context.clearRect(0, 0, imageWidth, imageHeight);
            context.drawImage(image, 0, 0, imageWidth, imageHeight);
        }
    }else{
        setScale(1024 / image.width, 1024 / image.height);
        resizeImage(scale);
    
    }
}

//投稿ボタンによる処理
function submitResizeFile() {
    var csrf_token_name = "csrfmiddlewaretoken"
    var csrf_hash = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    if (image !== null && fixFileObject !== null) {

        setScale(1024 / image.width, 1024 / image.height);
    
        var imageWidth = parseInt(image.width * scale, 10);
        var imageHeight = parseInt(image.height * scale, 10);
        canvas.width = imageWidth;
        canvas.height = imageHeight;
        context.clearRect(0, 0, imageWidth, imageHeight);
        context.drawImage(image, 0, 0, imageWidth, imageHeight);
    

        var resizeFileObject = null;

            // サイズ変更があった場合だけ送信用ファイルを作成
            var image64Data = canvas.toDataURL(fixFileObject.type);
            image64Data = image64Data.split(',')[1];
            imageData = atob(image64Data);
            var unit8Array = new Uint8Array(imageData.length);
            unit8Array.forEach(function(element, index) {
                unit8Array[index] = imageData.charCodeAt(index);
            });
            resizeFileObject = new File(
                [unit8Array],
                fixFileObject.name,
                {
                    type: fixFileObject.type
                }
            );
        

        var formData = new FormData();
        formData.append(csrf_token_name, csrf_hash);
        formData.append("file", resizeFileObject); //ここに入れるのを、512サイズのものにする
        formData.append("comment", document.getElementById("id_comment").value)
        formData.append("cafe", document.getElementById("id_cafe").value)

        // input type file の 値はjavascriptで上書き出来ないのでajaxで送信する
        //応答があった場合の命令
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    //csrf_hash = JSON.parse(xhr.response).csrf_hash;
                    messageArea.innerHTML = '<span style="color: green;">ファイルの送信に成功しました。</span>';
                    location.href = '/list';
                } else {
                    messageArea.innerHTML = '<span style="color: red;">ファイルの送信に失敗しました。</span>';
                }
            }
        }
        console.log(scale)
        //送信してくださいという命令。JSはリクエストが送れと命令した瞬間にリクエストが送られる
        xhr.open("POST", "/post_new_post");
        xhr.send(formData);
    }
}
}

// カフェ紹介ページ


function entryMapPage(){
    
    function extractCafeID(path) {
        /*
        / 正規表現開始記号
        . 任意の一文字にマッチ
        * 直前の正規表現0~n文字にマッチ
        \ 次の文字をエスケープ
        / /にマッチ
        ( グルーピング開始記号
        \d 任意の数字一文字にマッチ
        + 直前の正規表現1~n文字にマッチ
        ) グルーピング終了記号
        / 正規表現終了記号
        */
        return path.match(/.*\/(\d+)/)[1];
    }
    
    var cafeID = extractCafeID(window.location.pathname);
    console.log(cafeID);
    

    
    function fetchCafeInfo(cafeID){
        fetch("/cafe_info/"+cafeID).then(function(response) {
            return response.json();
          })
          .then(function(myJson) {
            console.log(myJson.latitude);
            var map = L.map('mapid').setView([myJson.latitude, myJson.longitude], 300); // setView(<LatLng> center, <Number> zoom, <Zoom/pan options> options?)
    //setViewのlatlngをminsta.models.Cafe.getbyid(...)のものを利用したい
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([myJson.latitude, myJson.longitude]).addTo(map) //L.marker(<LatLng> latlng, <Marker options> options?)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
        .openPopup();
          });
    }
    fetchCafeInfo(cafeID);
            
}

function entryCafeListPage(){
    const cafe_id = document.getElementById("cafe_id");
}



//user_page

function pop(self) {
    $('#imagepreview').attr('src', $(self).attr('src'));
    $('#imagemodal').modal('show');
}

function router(path){
    if(path === '/post_new_post'){
        entryPostPage();
        console.log("rrrrrrrrrrr");
    }
    else if((/.*\/(\d+)(\b)/).test(path)){
        entryMapPage(); 
        console.log("bbbbb");
    }
}


router(window.location.pathname)



//ユーザーページ
// https://www.w3schools.com/howto/howto_css_modal_images.asp

