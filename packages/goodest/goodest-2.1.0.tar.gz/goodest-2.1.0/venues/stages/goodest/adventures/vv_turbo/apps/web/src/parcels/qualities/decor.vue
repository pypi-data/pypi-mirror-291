







<script>

import { decor } from './decor.js'
export default decor

</script>


<template v-slot="slotProps" v-slot:default="slotProps">
	<lounge #default="{ palette, terrain }">
		<div
			ref="foundation"
			:style="{
				width: '100%',
				borderRadius: '12px',
				overflow: 'hidden'
			}"
		>
			<div
				
				:style="{
					padding: '.2in',
					maxWidth: '1000px',
					margin: '0 auto'
				}"
			>
				<header
					:style="{ 
						textAlign: 'center',
						padding: '0.5cm',
						
					}"
				>
					<h1
						:style="{
							fontSize: '2em'
						}"
					>Qualities</h1>
					<div :style="{ height: '0.2cm' }"></div>
					<p>These are the qualities of the platform.</p>
				</header>
			
				<s_panel
					:style="{ 
						textAlign: 'center',
						padding: '0.5cm'
					}"
				>
					<h1>Outline</h1>
					<div :style="{ height: '0.2cm' }"></div>
					<p>This platform shows the nutrient composition for groceries.</p>
					<div :style="{ height: '0.2cm' }"></div>					
					<p><b>Goals</b> is where a nutrion goal can be picked.</p>
					<div :style="{ height: '0.2cm' }"></div>					
					<p><b>Presents</b> shows the aggregate nutrient composition of groceries.</p>
					<div :style="{ height: '0.2cm' }"></div>					
					<p><b>Journal</b> has notes about veganism, health, etc.</p>
				</s_panel>
				
				<div :style="{ height: '20px' }" />



				<custom_physics 
					:style="{
						padding: '.25in'
					}"
				/>
				<div :style="{ height: '20px' }" />
				
				<generic_physics 
					:style="{
						padding: '.25in'
					}"
				/>
				<div :style="{ height: '20px' }" />
				
				<s_panel>
					
				
					<physics />
				</s_panel>
				
				<div :style="{ height: '20px' }" />
				
				
			</div>
		</div>
	</lounge>
</template>
