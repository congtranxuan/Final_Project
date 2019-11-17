$('document').ready(function () {
    $("#imgload").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                console.log("reader.onload");
                $('#imgshow').attr('src', e.target.result);
                $('#imgtext').attr('value', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
});