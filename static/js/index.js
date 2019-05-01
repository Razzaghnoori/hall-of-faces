var $form = $("#mainForm");
var $file = $("#file");
var inpImg = $(".inpImg");
var result_name = $(".name")

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
            var blobFile = input.files[0];
            var inp_img_url = URL.createObjectURL(blobFile);
            console.log(blobFile);
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
                json_resp = JSON.parse(response);
                inpImg.attr("src", json_resp.url);
                result_name.text(json_resp.name); 
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

  
$file.on('change', function(){
  readURL(this);
});