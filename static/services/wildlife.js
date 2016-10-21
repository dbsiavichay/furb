(function () {
  angular.module('wildlife.services', [
    'ngResource',
  ])

  .factory('Kind', function ($resource) {
    return $resource('/api/kinds/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    });
  })
  .factory('Breed', function ($resource) {
    return $resource('/api/breeds/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    });
  });
})();
