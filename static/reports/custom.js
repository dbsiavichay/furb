$(function () {
	var parish;

	$('select').on('change', function (e) {
		parish = $(this).val();
	})

	$('.btn-danger').on('click', function () {
		if (!parish) return; 
		var url = '/by_parish/'+ parish + '/report/';
		$('iframe').attr('src', url);
	});
});