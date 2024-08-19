

<script>

//
//	goals, advice, 
//

import { room } from './room'
export default room;

</script>


<template>
	<lounge #default="{ palette, terrain }">
		<div
			:style="{
				display: 'flex',
				height: '100%',
				flexDirection: 'column'						
			}"
		>
			<div
				:style="{
					padding: '1cm 0',
					textAlign: 'center'
				}"
			>
				<h1
					:style="{
						fontSize: '2em'
					}"
				>Goals</h1>
				<div :style="{ height: '0.2cm' }" />
				<p>This is where nutrition goals can be chosen.</p>
			</div>
		
			<s_panel
				:style="{
					margin: '10px 0',
					padding: '2px 16px'
				}"
			>
				<p>Goal Chosen:</p>
				
				<div
					:style="{
						display: 'flex',
						justifyContent: 'space-between',
						alignItems: 'center'
					}"
				>
					<h1>{{ this.find_label () }}</h1>
					
					<div>
						<s_button
							:clicked="erase_goal"
							:pressable="goal_picked"
							boundaries="8px 32px"
						>unpick</s_button>
						
						<s_button
							:clicked="open_goal"
							:pressable="goal_picked"
							boundaries="8px 32px"
						>details</s_button>
					</div>
				</div>
			</s_panel>
						
			<div
				:style="{
					height: '10px'
				}"
			/>
			
			<s_panel
				:style="{
					// height: '100%',
					padding: '2px 16px'
				}"
			>
				<h1 
					:style="{
						padding: '16px 0px',
						textAlign: 'center'
					}"
				>Possibilities</h1>
			
				<div 
					v-for="goal_data in goals"
					:style="{
						borderRadius: '4px',
						boxSizing: 'border-box',
						border: '2px solid ' + palette['6'],
						padding: '.25in'
					}"
				>
					<goal_furniture 
						:goal="goal_data" 
						:pick="pick" 
						:show_pick="true" 
						:show_goal="true" 
					/>
				</div>
				<div 
					v-if="
						!Array.isArray (goals) || 
						(Array.isArray (goals) && goals.length === 0)
					"
					
					:style="{
						borderRadius: '4px',
						boxSizing: 'border-box',
						border: '2px solid ' + palette['6'],
						padding: '.25in'
					}"
				>
					No goal options were found.				
				</div>				
			</s_panel>
		</div>
	</lounge>
</template>