

<script>

/*
	electricyte
*/

import mural from '@/scenery/name/mural.vue'
import router_link_scenery from '@/scenery/router_link/decor.vue'	
import { calc_address } from '@/fleet/calc_address'
	

export default {
	components: { mural, router_link_scenery },
	props: [],
	
	data () {
		// Ardor
		
		const address = calc_address ()
		
		return {
			// 
			//sun_flowers: `url("${ address }bits/2\/pexels-peter-de-vink-288978-849403.jpg")`,
			sun_flowers: `url("${ address }bits/4\/CharlVera--ai-generated-8084486_1920.jpg")`,
			
			text2: `B12 supplements and Omega 3, 6, 9 supplements are usually recommended for vegan diets.`,
			text3: `A vegan multivitamin is usually recommended as well.`
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
						transform: 'translateX(-50%)',
						
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
						
						backgroundImage: sun_flowers,
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
						
						top: '40px',
						
						position: 'relative',
						// top: '50%',
						left: '50%',
						// transform: 'translateX(-50%) translateY(-50%)',
						transform: 'translateX(-50%)',
						
						maxWidth: '1100px',
						width: '95%',
						//paddingTop: '3in'
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
						<p
							:style="{
								fontSize: '3em',
								marginBottom: '0.1cm'
							}"
						>
							<span :style="{ fontSize: '1.4em' }">
								<b>algae, plants, & fungi</b> 
							</span>						
						</p>
						<p
							:style="{
								fontSize: '2em'
							}"
						>
							<span :style="{ display: 'block' }">
								likely have every nutrient necessary for homo sapiens to flourish.
							</span>
						</p>
					</section>
					
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px',
							
							lineHeight: '2em'
						}"
					>
						<p
							:style="{
								fontSize: '2em',
								marginBottom: '0.1cm',
								fontWeight: 'bold'
							}"
						>Similar Genetics</p>
						<p
							:style="{
								fontSize: '1.5em'
							}"
						>There are mostly herbivorous animals with similar genetics to homo sapiens.</p>
						<p
							:style="{
								fontSize: '1.5em'
							}"
						><b>Silverback Gorillas</b> eat around ~99% herbs and ~1% meat on average.</p>
						<p
							:style="{
								fontSize: '1.5em'
							}"
						><b>Chimpanzees</b> eat around ~97% herbs and ~3% meat on average.</p>
					</section>
					
					<section
						:style="{
							marginTop: '12px',
							
							background: palette [1],
							border: '2px solid ' + palette [6],
							borderRadius: '4px',
							padding: '8px 31px',
							
							display: 'grid',
							'grid-template-columns': 'repeat(auto-fit, minmax(250px, 1fr))',
							'grid-auto-flow': 'dense',
							gap: '0.1cm'
						}"
					>
						<h2
							:style="{
								fontSize: '2em',
								fontWeight: 'bold'
							}"
						>@Veganism</h2>
						<h2
							:style="{
								fontSize: '2em',
								fontWeight: 'bold'
							}"
						>@Herbs</h2>
						<h2
							:style="{
								fontSize: '2em',
								fontWeight: 'bold'
							}"
						>@Mercyism</h2>
					</section>
				</article>
			</main>
		</s_panel>
	</lounge>
</template>

