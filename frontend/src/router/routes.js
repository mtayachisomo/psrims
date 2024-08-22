import ThanksSituationAnalysis from 'src/pages/ThanksSituationAnalysis.vue';
import ThanksReformAreaConfig from 'src/pages/ThanksReformAreaConfig.vue';
import ThanksReformWeights from 'src/pages/ThanksReformWeights.vue';


const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [

      {path: '/dashboard', component: () => import('pages/Dashboard2.vue')},
      {path: '/SituationAnalysis', component: () => import('pages/SituationAnalysis.vue')},
      {path: '/SituationAnalysis/thanks', name: 'ThanksSituationAnalysis', component: ThanksSituationAnalysis },
      {path: '/BlankPage', component: () => import('pages/blankpage.vue')},
      {path: '/institutionprofile', component: () => import('pages/institutionprofile.vue')},
      {path: '/M&E-output-graphs', component: () => import('pages/output.vue')},
      {path: '/MM&E-Outcome-graphs', component: () => import('pages/outcomes.vue')},
      {path: '/reformareaweight', component: () => import('pages/reformareaweight.vue')},
      {path: '/ThanksReformWeights/thanks', name: 'ThanksReformWeights', component: ThanksReformWeights },
      {path: '/reformareaconfigurations', component: () => import('pages/reformareaconfigurations.vue')},
      {path: '/ReformAreaConfig/thanks', name: 'ThanksReformAreaConfig', component: ThanksReformAreaConfig },
      {path: '/m&eframework/outputplan', component: () => import('pages/m&eframework/outputplan.vue')},
      {path: '/m&eframework/outcomeplan', component: () => import('pages/m&eframework/outcomeplan.vue')},
      {path: '/m&eframework/reporting/output', component: () => import('pages/m&eframework/reporting/output.vue')},
      {path: '/m&eframework/reporting/output&outcome', component: () => import('pages/m&eframework/reporting/output&outcome.vue')},
      {path: '/commitments', component: () => import('pages/commitments.vue')},
      {path: '/contract', component: () => import('pages/contract.vue')},
      {path: '/report', component: () => import('pages/report.vue')},
      {path: '/users/create', component: () => import('pages/users/createuser.vue')},
      {path: '/help/secretariat', component: () => import('pages/help.vue')},

    ]
  },


  {
    path: '',
    component: () => import('pages/Login-1.vue')
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  },



]

export default routes
