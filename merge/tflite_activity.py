
def realtime_count(Cpx,Cpy,Bpx,Bpy,realtime):
    global realtime
    if abs(Cpx - Bpx) >=15 or abs(Cpy-Bpy) >=15:
        realtime+=1
    return realtime