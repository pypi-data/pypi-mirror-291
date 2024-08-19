

<script>

/*
	This is the mobile nav?
*/

import { decor } from './decor'
export default decor;

</script>

<template>
	<lounge #default="{ palette, terrain, cart }">
		<nav>
			<router_link_scenery name="Qualities" :clicked="link_clicked" :style="{ textAlign: 'center' }" />
			<router_link_scenery name="Goals" :style="{ textAlign: 'center' }"/>
			<router_link_scenery 
				name="Presents"
				:has_slot="true"
				:clicked="link_clicked"
				:style="{ textAlign: 'center' }"
			>
				<span>Presents</span>
				<span
					:style="{
						marginLeft: '8px',
						padding: '2px 8px',
						borderRadius: '20px',
					}"
				>{{ cart.IDs.length }}</span>
			</router_link_scenery>
			
						
			<router_link_scenery name="Journal" :clicked="link_clicked" :style="{ textAlign: 'center' }"/>
			<router_link_scenery 
				name="Inventory" 

				:clicked="link_clicked" 
				:style="{ textAlign: 'center' }"
			/>
		
			<!-- groceries for herbivores -->
		
			<s_button
				ref="button"
				:pressable="true"
				boundaries="3px 12px 3px"
				:clicked="open_business"
				
				animation="1"
				
				:styles="{
					outside: {
						width: '100%',
					},
					inside: {}
				}"
			>
				Business
			</s_button>
			
			
		
			

		
		</nav>
	</lounge>
</template>