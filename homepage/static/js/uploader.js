tinymce.init({
      selector: "textarea#id_body",      
      height: "300",
      width: "100%",
      plugins: "insertdatetime  media image preview emoticons  directionality link  codesample contextmenu table code lists fullscreen ",
      toolbar: " image media emoticons|undo redo |  bold italic | preview | alignleft alignright aligncenter alignjustify",
      image_title: true,
      image_caption: true,
      automatic_uploads: true,
      image_advtab: true,
      file_picker_types: "file image media emoticons",

      file_picker_callback: function (cb, value, meta) {
           var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");}
        if (meta.filetype == "media") {
        input.setAttribute("accept", "video/*");}
		


        input.onchange = function () {     
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache =  tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
               cb(blobInfo.blobUri(), { title: file.name });
             };
             reader.readAsDataURL(file);
         };
         input.click();
      },
      content_style: "body { font-family:Helvetica,Arial,sans-serif; font-size:35px }"
  });
			   