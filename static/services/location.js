(function () {
  angular.module('location.services', [
    'ngResource',
  ])

  .factory('Parish', function ($resource) {
    return $resource('/api/parishes/:code/', {
      code: '@code'
    },{
      update: {method: 'PUT'}
    });
  })
  .factory('Owner', function ($resource) {
    return $resource('/api/owners/:charter/', {
      charter: '@charter'
    },{
      update: {method: 'PUT'}
    });
  })
  .factory('RegistroCivil', function ($resource) {
    return $resource('/api/civil-record/:charter/', {
      charter: '@charter'
    });
  });
})();
