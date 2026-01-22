from fastapi import FastAPI
app = FastAPI()
def get_my_status(month_salary):
    my_goal_salary =12000
    my_current_deposit =1000
    my_comment = ""
    for t in month_salary:
        my_current_deposit = t+ my_current_deposit
        if my_current_deposit>=30000:
            print("快攒够了")
            my_comment = "快攒够了！加油！"
        else:
            print("还得努力")
            my_comment = "还差一点，继续努力"
    return{
        "status":"success",
        "current_deposit":my_current_deposit,
        "goal_salary":my_goal_salary,
        "message": my_comment
    }           
@app.get("/")
def home():
    return{"message:":"你好这是我自己做的第一个ai服务后台"}
@app.get("/my_job_plan")
def check_month_salary():
    fake_data=[11000,10000,14000]
    result =get_my_status(fake_data)
    return result