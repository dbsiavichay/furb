(function () {
  angular.module('veterinary.controllers', [
    'veterinary.services',
    'wildlife.services'
  ])

  .controller('VaccineController', function ($scope, Vaccine, Kind) {
    $scope.vaccines = Vaccine.query();
    $scope.vaccine = null;
    $scope.kinds = Kind.query();

    $scope.edit = function (vaccine) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.vaccine = angular.copy(vaccine) || new Vaccine();
      if(!$scope.vaccine.kinds) $scope.vaccine.kinds = [];
    }

    $scope.remove = function (vaccine) {
      $scope.vaccine = vaccine;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.vaccine = null;
    }

    $scope.create = function () {
      $scope.flagKinds = $scope.vaccine.kinds.length > 0?false:true;
      if(!$scope.form.$valid || $scope.flagKinds) return;

      $scope.vaccine
        .$save(function (response) {
          $scope.vaccines.push($scope.vaccine);
          $scope.reset();
        });
    }

    $scope.update = function () {
      $scope.flagKinds = $scope.vaccine.kinds.length > 0?false:true;
      if(!$scope.form.$valid || $scope.flagKinds) return;

      $scope.vaccine
        .$update(function (response) {
          var index = getIndex($scope.vaccine);
          $scope.vaccines[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.vaccine
        .$remove(function () {
          var index = getIndex($scope.vaccine);
          $scope.vaccines.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    $scope.toggleKindSelection = function (id) {
      var index = $scope.vaccine.kinds.indexOf(id);
      if (index > -1) $scope.vaccine.kinds.splice(index, 1);
      else $scope.vaccine.kinds.push(id);
    }

    getIndex = function (vaccine) {
      for(var i in $scope.vaccines) {
        var t = $scope.vaccines[i];
        if(t.id === vaccine.id) return i;
      }
    }
  })
  .controller('DiseaseController', function ($scope, Disease, Kind) {
    $scope.diseases = Disease.query();
    $scope.disease = null;
    $scope.kinds = Kind.query();

    $scope.edit = function (disease) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.disease = angular.copy(disease) || new Disease();
      if(!$scope.disease.kinds) $scope.disease.kinds = [];
    }

    $scope.remove = function (disease) {
      $scope.disease = disease;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.disease = null;
    }

    $scope.create = function () {
      $scope.flagKinds = $scope.disease.kinds.length > 0?false:true;
      if(!$scope.form.$valid || $scope.flagKinds) return;

      $scope.disease
        .$save(function (response) {
          $scope.diseases.push($scope.disease);
          $scope.reset();
        });
    }

    $scope.update = function () {
      $scope.flagKinds = $scope.disease.kinds.length > 0?false:true;
      if(!$scope.form.$valid || $scope.flagKinds) return;

      $scope.disease
        .$update(function (response) {
          var index = getIndex($scope.disease);
          $scope.diseases[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.disease
        .$remove(function () {
          var index = getIndex($scope.disease);
          $scope.diseases.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    $scope.toggleKindSelection = function (id) {
      var index = $scope.disease.kinds.indexOf(id);
      if (index > -1) $scope.disease.kinds.splice(index, 1);
      else $scope.disease.kinds.push(id);
    }

    getIndex = function (disease) {
      for(var i in $scope.diseases) {
        var t = $scope.diseases[i];
        if(t.id === disease.id) return i;
      }
    }
  });
})();
