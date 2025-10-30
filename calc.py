def calculate_stats(attended, total, target):
    """Calculates current attendance percentage and status."""
    if total <= 0:
        return {'current_pct': 0.0, 'status': 'No classes held yet.'}
    
    current_pct = (attended / total) * 100
    
    status = 'Risk'
    if current_pct >= target:
        status = 'On Track'
    elif current_pct >= (target - 5):
        status = 'Warning'
        
    return {
        'current_pct': current_pct,
        'status': status,
        'attended': attended,
        'total': total,
        'target': target
    }

def calculate_prediction(current_pct, attended, total, target):
    """
    Predicts the number of classes to attend/miss to meet the target.
    
    NOTE: This function assumes the calling function (app.py) has already
    validated that target, attended, and total are valid numbers.
    """
    
    target_count = (target / 100) * total

    if current_pct >= target:
       
        missable_classes = 0
        future_total = total
        future_attended = attended
        
        while future_attended / future_total * 100 >= target:
            missable_classes += 1
            future_total += 1
            
            if missable_classes > 200: 
                missable_classes = "many"
                break
                
        
        if missable_classes != "many" and missable_classes > 0:
            missable_classes -= 1
            
        action_message = f"You are **On Track**! You can safely miss up to **{missable_classes}** upcoming classes while maintaining a {target}% attendance."
        
    else:
        
        required_to_attend = 0
        future_total = total
        future_attended = attended
        
       
        while future_attended / future_total * 100 < target:
            required_to_attend += 1
            future_attended += 1
            future_total += 1
            
            
            if required_to_attend > 200:
                required_to_attend = "many"
                break
        
        if required_to_attend == "many":
             action_message = f"You are far behind. You need to attend **all** of the next 200+ classes to reach {target}%."
        else:
            action_message = f"You need to attend the next **{required_to_attend}** consecutive classes to raise your attendance to {target}%."
            
    return {
        'action_needed': action_message
    }
