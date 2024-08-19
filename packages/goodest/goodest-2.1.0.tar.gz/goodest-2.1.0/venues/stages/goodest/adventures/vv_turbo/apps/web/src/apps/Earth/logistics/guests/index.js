

import { createRouter, createWebHistory } from 'vue-router'

import journal from '@/regions/guests/journal/decor.vue'

// var intro_path = "/@/"
var intro_path = "/front/@/"
var intro_path_s1 = "/@@/"

export const guests_routes = [
	{
		name: 'Journal',
		path: '/',
		component: journal
	},
	{
		name: 'Inventory',
		path: intro_path + 'herbs',
		component: () => import ('@/regions/guests/inventory/decor.vue')
	},
	{
		name: 'Qualities',
		path: intro_path + 'qualities',
		component: () => import ('@/parcels/qualities/decor.vue')
	},

	{
		name: 'food',
		path: intro_path + 'food/:emblem',
		component: () => import ('@/regions/guests/food/decor.vue')
	},
	{
		name: 'supp',
		path: intro_path + 'supp/:emblem',
		component: () => import ('@/regions/guests/supp/decor.vue')
	},	
	{
		name: 'meal',
		path: intro_path + 'meal/:emblem',
		component: () => import ('@/regions/guests/meal/decor.vue')
	},	
	
	//--
	//
	//	customs
	//
	{
		name: 'Goals',
		path: intro_path + 'goals',
		component: () => import ('@/regions/guests/goals/room.vue'),
		children: []
	},
	{
		name: 'Presents',
		path: intro_path + 'presents',
		component: () => import ('@/regions/guests/cart/decor.vue'),
		children: []
	},
	{
		name: 'account',
		path: intro_path + 'account',
		component: () => import ('@/regions/guests/account/decor.vue'),
		children: []
	},
	
	//--
	
	{
		name: 'meals',
		path: intro_path + 'meals',
		component: () => import ('@/regions/guests/meals/decor.vue')
	},	
	{
		name: 'map',
		path: intro_path + 'map',
		component: () => import ('@/regions/guests/map/decor.vue')
	},
	
	//--
	
	{
		name: 'navigation lab',
		path: intro_path_s1 + 'navigation-lab',
		component: () => import ('@/parcels/navigation-lab/field.vue')
	},
	{
		name: 'comparisons',
		path: intro_path_s1 + 'comparisons',
		component: () => import ('@/regions/guests/comparisons/region.vue')
	},
	
	//--
	
	{
		name: 'emblem',
		path: intro_path_s1 + 'emblem',
		component: () => import ('@/regions/guests/emblem/decor.vue')
	},	
]