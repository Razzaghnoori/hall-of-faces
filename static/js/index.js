function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
            $uploadedImg[0].style.backgroundImage='url('+e.target.result+')';
            var blobFile = input.files[0];
            var formData = new FormData();
            formData.append("fileToUpload", blobFile);
            console.log('mew');
            $.ajax({
               url: "/upload",
               type: "POST",
               data: formData,
               processData: false,
               contentType: false,
               success: function(response) {
                  var my_str = "I won!!!";
                  $("#resultsContainer").html = my_str;
               },
               error: function(jqXHR, textStatus, errorMessage) {
                   console.log('khor');
                   console.log(errorMessage); // Optional
               }
            });
        };

    reader.readAsDataURL(input.files[0]);
  }
}

var $form = $("#imageUploadForm"), 
    $file = $("#file"), 
    $uploadedImg = $("#uploadedImg"), 
    $helpText = $("#helpText")
;
$file.on('change', function(){
  readURL(this);
  $form.addClass('loading');
});
$uploadedImg.on('webkitAnimationEnd MSAnimationEnd oAnimationEnd animationend', function(){
  $form.addClass('loaded');
});
$helpText.on('webkitAnimationEnd MSAnimationEnd oAnimationEnd animationend', function(){
  setTimeout(function() {
    $file.val('');
    $form.removeClass('loading').removeClass('loaded');
  }, 5000);
});

function uploadFile() {
    var blobFile = $('#file').files[0];
    var formData = new FormData();
    formData.append("file", blobFile);
    console.log('mew');
    $.ajax({
       url: "/upload",
       type: "POST",
       data: formData,
       cache: false,
       processData: false,
       contentType: false,
       success: function(response) {
           console.log('uploaded successfully')
       },
       error: function(jqXHR, textStatus, errorMessage) {
           console.log('khor');
           console.log(errorMessage); // Optional
       }
    });
}