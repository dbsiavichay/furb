(function () {
  angular.module('location.controllers', [
    'location.services'
  ])
  .controller('OwnerController', function ($scope, $location, Owner, Parish, RegistroCivil) {
    $scope.parishes = Parish.query();
    $scope.owner = null;
    $scope.error = false;
    $scope.errorMessage;
    $scope.state = 'read';

    $scope.search = function ($event) {
      if($event) {
        if($event.keyCode!=13) return;
      }

      $scope.error = !validateCharter($scope.owner.charter);
      if ($scope.error) {
        var charter = $scope.owner.charter;
        $scope.errorMessage = 'La cédula ingresada es incorrecta.';
        $scope.owner = new Owner();
        $scope.owner.charter = charter;
        return;
      };

      Owner.get({'charter': $scope.owner.charter}, function (response) {
        $scope.owner = angular.copy(response);
        $scope.state = 'update';
      }, function (error) {
        if(error.status==404) {
          RegistroCivil.get({'charter':$scope.owner.charter}, function (response) {
            var charter = $scope.owner.charter;
            $scope.owner = new Owner();
            $scope.owner.charter = charter;

            if(response.CodigoError=='001') {
              $scope.error = true;
              $scope.errorMessage = 'La cédula ingresada no existe';
              return;
            }

            $scope.owner.name = response.Nombre;
            $scope.state = 'create';
          });
        }
      });
    }

    $scope.create = function () {
      if(!$scope.form.$valid) return;

      $scope.owner.real_charter = $scope.owner.charter;
      $scope.owner.charter = null;
      $scope.owner
        .$save(function (response) {
          $scope.owner = angular.copy(response);
          $location.path('/animales/'+ $scope.owner.charter);
        });
    }

    $scope.update = function () {
      if(!$scope.form.$valid) return;

      $scope.owner
        .$update(function (response) {
          $location.path('/animales/'+ response.charter);
        });
    }


    validateCharter = function (charter) {
      var array = charter.split('');

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

  });
})();
