



<script>

import mural from '@/scenery/name/mural.vue'
import { calc_address } from '@/fleet/calc_address'

export default {
	components: { mural },
	props: [],
	
	data () {
		return {
			// 
			tractor: `url("\/bits/1\/Samuelsp--ai-generated-8440480_1920.png")`,
			
			universe: `url("\/bits/1\/universe.png")`,
			pitachios: `url("\/bits/1\/NoName_13--pistachios-1540123_1920.jpg")`,

			title: "Mercifulness (Mercyism)",			
			// title: "Goodness",
			// title: "Limits",			
			// slogan: "There's lines that shouldn't be crossed.",
			
			slogan: "Mercy towards other species is now very easy with contemporary agriculture, logistics, and nutrition science.",
			
			
			//slogan: "Be good towards other species unless necessity requires otherwise.",
			//slogan: "You probably don't want to know what goes on in the non-goodest food industry.",
			//slogan2: "It's not as nice as it was in the past.",
		}
	}
}

</script>


<template>
	<lounge #default="{ palette, style, terrain }">
		<s_panel
			:style="Object.assign ({}, {
				minHeight: '100vh',
				fontSize: terrain.width <= terrain.mobile_nav_width ? '.7em' : '1em'
			}, style)"
			:board_physics="{
				minHeight: '100vh',
			}"
		>		
			<main
				:style="{
					display: 'flex',
					
					position: 'relative',
					top: 0,
					left: 0,

					boxSizing: 'border-box',
					minHeight: '100vh',
					height: '100%',
					width: '100%',
					padding: '.5in 0',
					
					textAlign: 'center',
					
					color: 				palette [2],
					transition: [
						'color ' 	  + palette.change_duration,
						'border '     + palette.change_duration,
					].join (', '),
				}"
			>		
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%) scaleX(-1)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						backgroundColor: 'white',						
					}"
				></div>
			
				<div
					:style="{
						position: 'absolute',
						top: '0',
						left: '50%',
						transform: 'translateX(-50%)',
						
						height: '100%',
						width: '100%',
						maxWidth: '1600px',
						
						backgroundImage: tractor,
						backgroundPosition: '23% 75%',
						backgroundRepeat: 'no-repeat',
						backgroundSize: 'cover',
						
						opacity: 1
					}"
				></div>
			

				

				<article
					:style="{
						display: 'flex',
						flexDirection: 'column',
						justifyContent: 'center',
						
						position: 'relative',
						left: '50%',
						transform: 'translateX(-50%)',
						
						maxWidth: '1000px',
						width: '90%'
					}"
				>
					<section
						:style="{
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '5em'
							}"
						>{{ title }}</h2>
					</section>
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '1.5em'
							}"
						>{{ slogan }}</h2>
					</section>
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px'
						}"
					>
						<h2
							:style="{
								fontSize: '1.5em'
							}"
						>Given two meal plans that have the same nutritional content, the one that contains organisms that display the least signs of feeling, movement, and aptitude might be the most ethical choice.</h2>
					</section>
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px',
							
							lineHeight: '1.2em'
						}"
					>
						<p
							:style="{
								fontSize: '1em'
							}"
						>Theoretically there could be advanced plants with central nervous systems, motor functions, and a range of feelings that was similar to homo sapiens.  Therefore, merciful eating probably supercedes veganism in the ethics competition.</p>						
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

