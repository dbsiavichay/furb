(function () {
  angular.module('wildlife.controllers', [
    'wildlife.services',
    'location.services'
  ])

  .controller('KindController', function ($scope, Kind) {
    $scope.kinds = Kind.query();
    $scope.kind = null;

    $scope.edit = function (kind) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.kind = angular.copy(kind) || new Kind();
    }

    $scope.remove = function (kind) {
      $scope.kind = kind;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.kind = null;
    }

    $scope.create = function () {
      if(!$scope.form.$valid) return;

      $scope.kind
        .$save(function (response) {
          $scope.kinds.push($scope.kind);
          $scope.reset();
        });
    }

    $scope.update = function () {
      if(!$scope.form.$valid) return;

      $scope.kind
        .$update(function (response) {
          var index = getIndex($scope.kind);
          $scope.kinds[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.kind
        .$remove(function () {
          var index = getIndex($scope.kind);
          $scope.kinds.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    getIndex = function (kind) {
      for(var i in $scope.kinds) {
        var t = $scope.kinds[i];
        if(t.id === kind.id) return i;
      }
    }
  })
  .controller('BreedController', function ($scope, Kind, Breed) {
    $scope.kinds = Kind.query();
    $scope.breeds = Breed.query();
    $scope.breed = null;

    $scope.edit = function (breed) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.breed = angular.copy(breed) || new Breed();
    }

    $scope.remove = function (breed) {
      $scope.breed = breed;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.breed = null;
    }

    $scope.create = function () {
      if(!$scope.form.$valid) return;

      $scope.breed
        .$save(function (response) {
          $scope.breeds.push($scope.breed);
          $scope.reset();
        });
    }

    $scope.update = function () {
      if(!$scope.form.$valid) return;

      $scope.breed
        .$update(function (response) {
          var index = getIndex($scope.breed);
          $scope.breeds[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.breed
        .$remove(function () {
          var index = getIndex($scope.breed);
          $scope.breeds.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    getIndex = function (breed) {
      for(var i in $scope.breeds) {
        var t = $scope.breeds[i];
        if(t.id === breed.id) return i;
      }
    }
  })
  .controller('AnimalController', function ($scope, $routeParams, $location, Kind, Breed, Animal, Parish) {
    $scope.parishes = Parish.query();
    $scope.kinds = Kind.query();
    $scope.breeds = [];
    $scope.animal = new Animal()
    $scope.animal.owner = $routeParams.owner;
    $scope.age = '';

    $scope.edit = function (animal) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.animal = angular.copy(animal) || new Animal();
    }

    $scope.remove = function (animal) {
      $scope.animal = animal;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.animal = null;
    }

    $scope.create = function () {
      if(!$scope.form.$valid) return;

      $scope.animal
        .$save(function (response) {
          $location.path('/animales-reporte/'+response.id)
        });
    }

    $scope.update = function () {
      if(!$scope.form.$valid) return;

      $scope.animal
        .$update(function (response) {
          var index = getIndex($scope.animal);
          $scope.animals[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.animal
        .$remove(function () {
          var index = getIndex($scope.animal);
          $scope.animals.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    $scope.loadBreeds = function () {
      $scope.breeds = Breed.query({'kind': $scope.animal.kind})
    }

    $scope.processAge = function () {
      if(!$scope.form.birthday.$valid) return;
      var age = ''

      var seconds = Math.floor((new Date() - $scope.animal.birthday) / 1000);

      var interval = Math.floor(seconds / 31536000);

      if (interval > 1) age = age + interval + ' años ';
      else if ((interval == 1)) age = age + interval + ' año ';


      seconds = seconds % 31536000;
      interval = Math.floor(seconds / 2592000);
      if (interval > 1) age = age + interval + ' meses ';
      else if (interval == 1) age = age + interval + ' mes ';

      seconds = seconds % 2592000;
      interval = Math.floor(seconds / 86400);
      if (interval > 1) age = age + interval + ' días ';
      else if (interval == 1) age = age + interval + ' día ';

      $scope.age = age;
    }

    processCode = function () {
      var a = $scope.animal;
      var code = a.parish;
      code += a.gender;
      code += a.kind>9?a.kind:'0'+a.kind;
      return code;
    }

    getIndex = function (animal) {
      for(var i in $scope.animals) {
        var t = $scope.animals[i];
        if(t.id === animal.id) return i;
      }
    }
  })
  .controller('AnimalReportController', function ($scope, $routeParams) {
    $scope.url = '/report/ficha/?animal=' + $routeParams.id        
  });
})();
