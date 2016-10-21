(function () {
  angular.module('wildlife.controllers', [
    'wildlife.services'
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
  });
})();
