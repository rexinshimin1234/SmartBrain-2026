import pdfplumber
def read_pdf(file_path):
    print(f"📖 正在尝试读取文件: {file_path}")
    text_content = []
    try:
        # 打开 PDF 文件
        with pdfplumber.open(file_path) as pdf:
            # 遍历每一页
            for i, page in enumerate(pdf.pages):
                print(f"   --> 正在扫描第 {i+1} 页...")
                text = page.extract_text()
            if text:
                    text_content.append(text)
                    print(f"       (提取到 {len(text)} 个字符)")
            else:
                    print("       (警告：这一页好像是图片或空的)")
                    
        return "\n".join(text_content)

    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return ""
if __name__ == "__main__":
    pdf_path = "./data/secret.pdf"
    
    content = read_pdf(pdf_path)
    
    print("\n--- 📝 提取到的最终内容 ---")
    print(content)
    print("---------------------------")
    
    if "深蓝" in content:
        print("✅ 成功！Python 已经读到了绝密情报！")
    else:
        print("❌ 失败！内容不对，请检查 PDF 是否是纯图片扫描件。")