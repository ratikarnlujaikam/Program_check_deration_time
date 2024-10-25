# ข้อมูลที่ได้รับมา
data = "K5500000084*3SFDB72856N*P205287100*EB*Q1056*GFDB72856N-M001-P00001*L2024-6*D06/26/2024*RHI-P/NV/HI-P*AFDB72856N*V14149*B*"

# แยกข้อมูลตามเครื่องหมาย '*'
split_data = data.split('*')

# ดึงข้อมูลที่อยู่หลังเครื่องหมาย '*' ตัวที่ 2 และเอาตัวอักษรตัวแรกออก
final_data = split_data[2][1:]
print("Final Data:", final_data)

# ดึงข้อมูลจาก split_data[8] และเอาตัวอักษรตัวแรกออก
ramp = split_data[8][1:]
print("Ramp:", ramp)

# ข้อมูลเพิ่มเติม
additional_data = """LONGSPEAK 10D|205287100 Rev.B|HI-P|Notion(NEW)|TALLER,|LSP5A460430|324|HI-P|5|"""
Splitadditional_data = additional_data.split('|')