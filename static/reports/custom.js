$(function () {
	var parish;

	$('select').on('change', function (e) {
		parish = $(this).val();
	})

	$('#byParish').on('click', function () {
		if (!parish) return; 
		var filter = $('#sterilized').is(':checked')?'?sterilized=true':'';

		var url = '/by_parish/'+ parish + '/report/'+filter;
		$('iframe').attr('src', url);
	});

	$('#btnStats').on('click', function () {
		var month = $('#month').val();
		var year = $('#year').val();

		if(!month || !year) return;

		var url = '/stats/report/'+ month + '/' + year + '/';
		$('iframe').attr('src', url);
	});
});