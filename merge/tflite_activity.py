
def realtime_count(Cpx,Cpy,Bpx,Bpy):
    if abs(Cpx - Bpx) >=2 or abs(Cpy-Bpy) >=2:
        return True
    else:
        return False
