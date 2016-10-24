(function () {
  var app = angular.module('furb', [
    'ngRoute',
    'wildlife.controllers',
    'veterinary.controllers',
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
      })
      .when('/animales', {
        templateUrl: 'static/views/wildlife/animals.html',
        controller: 'AnimalController'
      })
      .when('/vacunas', {
        templateUrl: 'static/views/veterinary/vaccines.html',
        controller: 'VaccineController'
      })
      .when('/enfermedades', {
        templateUrl: 'static/views/veterinary/diseases.html',
        controller: 'DiseaseController'
      })
      .otherwise({
        redirectTo: '/'
      });

    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);
})();
