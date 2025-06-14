import streamlit as st

# Initialize session state for to-do items if it doesn't exist
if 'todo_items' not in st.session_state:
    st.session_state.todo_items = []

# App title
st.title("📝 To-Do List")
st.markdown("---")

# Add new to-do item section
st.subheader("Add New Task")
with st.form("add_task_form"):
    new_task = st.text_input("Enter a new task:", placeholder="Type your task here...")
    submitted = st.form_submit_button("Add Task")
    
    if submitted:
        if new_task.strip():  # Check if task is not empty or just whitespace
            # Add new task to session state
            st.session_state.todo_items.append({
                'task': new_task.strip(),
                'completed': False
            })
            st.success(f"Added task: {new_task.strip()}")
            st.rerun()
        else:
            st.error("Please enter a valid task!")

st.markdown("---")

# Display to-do items section
st.subheader("Your Tasks")

if len(st.session_state.todo_items) == 0:
    st.info("No tasks yet! Add your first task above.")
else:
    # Reset all button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Reset All", help="Mark all tasks as not done"):
            for item in st.session_state.todo_items:
                item['completed'] = False
            st.success("All tasks reset to not done!")
            st.rerun()
    
    st.markdown("### Task List")
    
    # Display each to-do item with checkbox
    for i, item in enumerate(st.session_state.todo_items):
        col1, col2, col3 = st.columns([0.5, 4, 1])
        
        with col1:
            # Checkbox for marking completion
            is_completed = st.checkbox(
                "", 
                value=item['completed'], 
                key=f"checkbox_{i}",
                help="Mark as done/not done"
            )
            
            # Update completion status if changed
            if is_completed != item['completed']:
                st.session_state.todo_items[i]['completed'] = is_completed
                st.rerun()
        
        with col2:
            # Display task text with strikethrough if completed
            if item['completed']:
                st.markdown(f"~~{item['task']}~~ ✅", help="Completed task")
            else:
                st.markdown(f"{item['task']}")
        
        with col3:
            # Delete button for each task
            if st.button("🗑️", key=f"delete_{i}", help="Delete this task"):
                st.session_state.todo_items.pop(i)
                st.success("Task deleted!")
                st.rerun()

# Display statistics
st.markdown("---")
if len(st.session_state.todo_items) > 0:
    completed_count = sum(1 for item in st.session_state.todo_items if item['completed'])
    total_count = len(st.session_state.todo_items)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", total_count)
    with col2:
        st.metric("Completed", completed_count)
    with col3:
        st.metric("Remaining", total_count - completed_count)
    
    # Progress bar
    if total_count > 0:
        progress = completed_count / total_count
        st.progress(progress)
        st.caption(f"Progress: {completed_count}/{total_count} tasks completed ({progress:.1%})")

# Footer
st.markdown("---")
st.caption("💡 Tip: Use the checkboxes to mark tasks as done, and the reset button to mark all tasks as not done.")
