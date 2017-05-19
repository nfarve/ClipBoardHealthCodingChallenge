/* eslint-disable global-require */
import 'dotenv/config';
import reactApp from './views/app';
import recordList from './api/records';
const routes = (app) => {

  /* example api route */
  app.get('/api/records', require('./api/records').all); 

  app.get('/api/records/department/:departmentid', recordList.departmentQuery);
  app.get('/api/records/education/:educationid', recordList.educationQuery);
  app.get('/api/records/salary/:direction/:salaryamount', recordList.salaryQuery);
  app.get('/api/records/patientToNurseRatio/:direction/:ratio', recordList.ratioQuery);
  app.get('/api/records/experience/:direction/:experience', recordList.experienceQuery);
  reactApp(app); // set up react routes
};

export default routes;
/* eslint-enable global-require */
