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
  });
})();
