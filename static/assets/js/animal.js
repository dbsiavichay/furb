$(function () {
	$('#id_charter').on('blur', function () {
		var charter = $(this).val();
		var formGroup = $('#charterInvalid').parents('.form-group');
		if (!isValid(charter)) {
			$('#charterInvalid').show();
			if (!formGroup.hasClass('has-error')) formGroup.addClass('has-error');
			return;
		}
		$('#charterInvalid').hide();
		formGroup.removeClass('has-error');

		$.get('/owner/'+charter+'/', function (data) {
			$('.form-control').each(function (index, element) {	
				$(element).val(data[$(element).attr('name')]);
			});
		}).fail(function (error) {
			$('.form-control').each(function (index, element) {	
				if($(element).attr('name')!='charter') $(element).val('');
			});
			if(error.status = 404) {
				$.get('/api/civil-record/'+charter+'/', function (response) {	
		            if(response.CodigoError=='001') {
		              	$('#charterInvalid').show();
						if (!formGroup.hasClass('has-error')) formGroup.addClass('has-error');
		              	return;
		            }		            
		            $('#id_name').val(response.Nombre) 
	          	});
			}
		});
	});
});

var isValid = function (charter) {
	var a = 1400234512
	var array = charter.split('');
	if (isNaN(charter)) return false;
	if (array.length != 10 ) return false;

	total = 0;
	digito = (array[9]*1);

	for( i=0; i < (array.length - 1); i++ ) {
	  mult = 0;
	  if ( ( i%2 ) != 0 ) {
	    total = total + ( array[i] * 1 );
	  } else {
	    mult = array[i] * 2;
	    if ( mult > 9 ) total = total + ( mult - 9 );
	    else total = total + mult;
	  }
	}

	decena = total / 10;
	decena = Math.floor( decena );
	decena = ( decena + 1 ) * 10;
	final = ( decena - total );
	if ( ( final == 10 && digito == 0 ) || ( final == digito ) ) {
	  return true;
	} else {
	  return false;
	}
}