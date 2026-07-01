import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import "./assets/style.css";

// Pages
import Home from "./pages/home/Home.vue";
import SurveyBuilder from "./pages/survey-builder/SurveyBuilder.vue";
import SurveyResponse from "./pages/survey-response/SurveyResponse.vue";
import Analytics from "./pages/Analytics.vue";

const routes = [
  { path: "/forms", component: Home, name: "Home" },
  { path: "/forms/new", component: SurveyBuilder, name: "NewSurvey" },
  { path: "/forms/edit/:name", component: SurveyBuilder, name: "EditSurvey" },
  { path: "/forms/analytics/:name", component: Analytics, name: "Analytics" },
  { path: "/survey/:code", component: SurveyResponse, name: "SurveyResponse" },
  { path: "/:pathMatch(.*)*", redirect: "/forms" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const pinia = createPinia();

const app = createApp(App);
app.use(pinia);
app.use(router);
app.mount("#app");
