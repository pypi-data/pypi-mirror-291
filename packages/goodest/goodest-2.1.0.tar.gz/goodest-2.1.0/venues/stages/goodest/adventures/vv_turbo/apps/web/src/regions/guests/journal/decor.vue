


<script>

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, style, terrain }">
		<div journal-region />
	
		<div
			:style="{
				padding: '2cm 0',
				textAlign: 'center'
			}"
		>
			<h1
				:style="{
					fontSize: '2em'
				}"
			>Journal</h1>
		</div>
	
		<!-- <panel_1 /> -->

		<panel_growing />
		<panel_health />
		<panel_goodness />
		
		<panel_moon />
		
		<!-- <panel_tech /> -->
		
		<panel_physics />
		



		<panel_sink />
	</lounge>
</template>
