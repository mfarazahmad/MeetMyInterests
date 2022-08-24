# Workout Data Models
 
## PROGRAM MODEL
 * Workout Name ['Faraz Bodyweight Program', 'Faraz Dumbell/Band Program', 'AthleanX Jacked/Elastx ', ' M&S PHUL', 'Coolcicada PPL' ]
 * Workout Type ['Calisthenics','Bro Split', 'Fullbody', 'Upper/ Lower', 'PPL']
 * Frequency [2, 3, 4, 5, 6]
 * PROGRAM_EXCERCISE(s) -> LIST of Objects []
 * 
## EXCERCISE MODEL
 * ID
 * Excercise Name ['Squat', 'Deadlift', 'Bench']
 * Excercise Type ['Push', 'Pull', 'Other']
 * Body Part ['Legs', 'Upper Back' 'Lower Back', 'Lats', 'Arms', 'Chest', 'Core']

## PROGRAM_EXCERCISE MODEL -> Inherits EXERCISE model
 * Excercise_ID
 * Recommended Volume (Reps * Weight)
 * Recommended Sets & Reps
 * Alternative Excercise -> Object
 * Band Weight Multiplier
 * Program Day
 * EQUIPMENT -> List of Strings []

## DAILY_TRACKER MODEL
 * Date
 * PROGRAM
 * EXCERCISE_LOG(s) -> List of Objects []
 * MEASUREMENTS
 * NUTRITION
 * Weight

## EXCERCISE_LOG MODEL
 * Excercise Name
 * Excercise ID
 * Sets [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
 * Reps [0-40]
 * Weight
 * Timing
 
## EQUIPMENT MODEL
 * ['Barbell', 'Dumbell', X3, 'BANDS' -> Object, 'Pullup-Bar', 'Bench', 'Pulley-System']
  
## BANDS MODEL
 * Band-Name ['Extra-Light', 'Light', 'Medium Light', 'Heavy','Very Heavy']
 * Band-Low-Weight [10, 25, 50, 60]
 * Band-Single-Weight [40, 50, 80, 120, 150]
 
## USER MODEL
 * Name
 * Email
 * Ethnicity (optional)
 * TDEE
 
## MEASUREMENTS MODEL
 * Height
 * Chest
 * Bicep
 * Tricep
 * Thights
 * Calves
 * Waist
 * Neck
  
## GOALS MODEL
 * MEASUREMENTS
 * EXCERCISE
 * NUTRITION
  
## NUTRITION MODEL
 * Calories
 * Protiens
 * Water
  
## STATISTICS MODEL
 * GROWTH BY EXCERCISE
 * GROWTH BY MEASUREMENT
 * VOLUME TRAJECTORY
 * BEST EXCERCISES