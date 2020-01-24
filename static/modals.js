    $(document).ready(function () {
        $('#feedbackModal').DataTable();
    });
    var modal = document.getElementsByClassName('.modal1');

    var span = document.getElementsByClassName(".close")[0];
     span.onclick = function() {
     modal.style.display = "none";}
     $(document).click(function (e) {
    if ($(e.target).is('.modal1')) {
        $('.modal1').fadeOut(500);
    }

});

$(".container").click(function () {
    $(".modal1").fadeOut(500);


});
$(".close").click(function () {
    $(".modal1").fadeOut(500);
});
$(".close-circle").click(function () {
    $(".modal").fadeOut(500);
});
     window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }

}
