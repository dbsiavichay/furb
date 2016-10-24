(function () {
  angular.module('veterinary.services', [
    'ngResource',
  ])

  .factory('Vaccine', function ($resource) {
    return $resource('/api/vaccines/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    });
  })
  .factory('Disease', function ($resource) {
    return $resource('/api/diseases/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    });
  });
})();
