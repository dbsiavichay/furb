$(function () {
	var parish;

	$('select').on('change', function (e) {
		parish = $(this).val();
	})

	$('.btn-danger').on('click', function () {
		if (!parish) return; 
		var filter = $('#sterilized').is(':checked')?'?sterilized=true':'';

		var url = '/by_parish/'+ parish + '/report/'+filter;
		$('iframe').attr('src', url);
	});
});