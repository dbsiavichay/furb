(function () {
  var app = angular.module('furb', [
    'ngRoute',
    'wildlife.controllers',
    'datatables'
  ]);

  app.config(['$routeProvider', '$resourceProvider', function ($routeProvider, $resourceProvider) {
    $routeProvider
      .when('/especies', {
        templateUrl: 'static/views/wildlife/kinds.html',
        controller: 'KindController'
      })
      .when('/razas', {
        templateUrl: 'static/views/wildlife/breeds.html',
        controller: 'BreedController'
      });

    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);
})();
