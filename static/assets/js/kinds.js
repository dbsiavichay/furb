$('.kind-icon').on('click', function () {
  $('.kind-icon').removeClass('selected');
  $(this).toggleClass('selected');
});


$('#btnSubmit').on('click', function () {
  var image = $('.selected').attr('icon');

  $('<input>').attr('type','hidden')
              .attr('name','image')
              .attr('value',image).appendTo('#form');
  $('#form').submit();
});
