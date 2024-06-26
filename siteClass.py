import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from clienteClass import Cliente
from emailClass import Email
from excelClass import Excel
from utilsClass import Utils
from autoGuiClass import AutoGui
from dotenv import load_dotenv

class Site:

    global driver   
    global runState
    global count
        
    driver = webdriver.Chrome() 
    load_dotenv()  

    def getChrome():        
        driver.get(os.getenv("url"))
        time.sleep(2)        
        driver.maximize_window()
        return driver
        
    def login():
        Site.getChrome()
        try:
            search = driver.find_element(By.XPATH, '//*[@id="login-container"]/form/fieldset/div[1]/div[1]/div/div/input')            
            time.sleep(1)        
            searchSecond = driver.find_element(By.XPATH, '//*[@id="senha"]')
            time.sleep(1)
            btnLogin = driver.find_element(By.XPATH, '//*[@id="btnLogin"]')

            if search is None or searchSecond is None or btnLogin is None:
                text ="Elemento da tela de login não encontrado."    
                Utils.writeLog(text,1)   
                raise
            try:    
                if search:
                    search.send_keys(os.getenv("user"))                       
                    time.sleep(1)         
                    if searchSecond:
                        searchSecond.send_keys(os.getenv("password"))
                        time.sleep(1)       
                        if btnLogin:
                            time.sleep(1)    
                            btnLogin.click()
                            time.sleep(2)                                                                           
                            Site.fillForm()         
            except:            
                text ='Falha ao inserir dados ou clicar para acessar'    
                Utils.writeLog(text,1) 
            raise    
        except:  
            time.sleep(5)
            driver.refresh()
            Site.login()

    def findNumber(nCarga, value):
        try:
            time.sleep(2)
            btnList = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[3]/div[1]/a[1]')
            btnList.click()
        except:
            text ='Não achei o botão da lista de CTE'
            Utils.writeLog(text,1)
        try:        
            time.sleep(4)
            nTable = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[5]/div/div/div/div[2]/div/table/tbody/tr[1]/td[2]').text
            Excel.insertExcelN(nCarga, nTable, value)  
        except:     
            text ='Não achei o botão de importar'
            Utils.writeLog(text,1)

    def importFile(file):              
        time.sleep(5)  
        try:
            btnCTe = driver.find_element(By.XPATH, '//*[@id="principalMenu"]/li[2]/a/i')
            if btnCTe:       
                    try:  
                        btnCTe.click()
                        time.sleep(1)
                        btnImport = driver.find_element(By.XPATH, '//*[@id="modal-opcoes-emissao"]/div/div/div[2]/div/div[1]/button/i') 
                    except Exception as e:                      
                        text ='Não achei o botão de importar'
                        Utils.writeLog(text,1)
                        raise

                    if btnImport:   
                        try:  
                            time.sleep(1)
                            btnImport.click()
                            time.sleep(1)
                            btnChoosefile = driver.find_element(By.XPATH,'//*[@id="dropzone"]/div')
                        except Exception as e:                         
                            text ='Não achei o botão de enviar arquivo'   
                            Utils.writeLog(text,1) 
                            raise
                        if btnChoosefile:  
                            try:      
                                btnChoosefile.click()
                                time.sleep(1)
                                AutoGui.importArchive(file)
                                time.sleep(1)
                                btnFImport = driver.find_element(By.XPATH,'//*[@id="btnImportarXML"]')
                                time.sleep(5)
                            except Exception as e:                            
                                text ='Não achei o botão depois de escolher o arquivo'    
                                Utils.writeLog(text,1)   
                                raise
                            if btnFImport:       
                                try:                     
                                    btnFImport.click()
                                    time.sleep(2)
                                except Exception as e: 
                                    text ='Não achei o botão de finalizar import'    
                                    Utils.writeLog(text,1)
                                    raise
            return True                    
        except Exception as e:
            return False

    def findAlert(xml, cliente):   
            try:     
                alert = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[3]/ul/li')
                if alert:
                    print(3) 
                    result = Utils.findText(alert.text)
                    print(result)                         
                    Email.sendEmailTeste(xml,cliente)                                                                        
                    print(1)  
                    return False    
            except:
                return True
            
             
            
    def fillForm():
        util = Utils()                
        for i in range(0,len(util.dir_list),1):     
            try:      
                try:                        
                    site = Site.importFile(util.dir_list[i])   
                    if site == False:
                        raise             
                    todayDay = Utils.getDay()

                    inputDate = driver.find_element(By.XPATH, '//*[@id="divData"]/div/div/div/input')
                    inputDateTwo = driver.find_element(By.XPATH, '//*[@id="dadosTipoCTe"]/div[1]/div/div/div/div[2]/div/div/div/input')
                    span = driver.find_element(By.XPATH, '//*[@id="abaSeguroDiv"]/div/div[1]/h4/span')
                

                    if inputDate is None or inputDateTwo is None:
                        text ='Elemento não encontrado na tela do Form'    
                        Utils.writeLog(text,1) 
                        raise

                        
                    if inputDate:                        
                        inputDate.send_keys(Keys.ENTER)
                        time.sleep(1)
                        if inputDateTwo:
                            inputDateTwo.send_keys(todayDay)                                
                            time.sleep(1)
                            span.click()
                except Exception as e:      
                    raise      
                try:
                        time.sleep(1)
                        spanball = driver.find_element(By.XPATH, '//*[@id="abaSeguroDiv"]/div/div[2]/div/div/div/div[1]/div/div/label[1]/span')
                        spanball.click()
                        time.sleep(1)
                        span.click()
                        time.sleep(1)
                        inputBall = driver.find_element(By.XPATH,'//*[@id="dadosTipoCTe"]/div[6]/div[2]/div/div/div[1]/div/div/label[2]/span')
                                                       
                  
                        if inputBall:
                            inputBall.click()
                            driver.execute_script("window.scrollTo(0, 2100);")
                            time.sleep(3)
                            inputValue = driver.find_element(By.XPATH, '//*[@id="subtotalPrestacao"]')
                except Exception as e:
                    raise 
                try:           
                    if inputValue:  
                        data = util.readXML(util.dir_list[i]) 
                        if data == None or data == 'nan':
                            raise        
                        client = Cliente(data)                                                 
                        info = client.searchCliente() 
                        if info == None or info == 'nan':
                            raise
                        time.sleep(1)                                    
                        inputValue.send_keys(info)                                      
                        time.sleep(1)
                        inputText = driver.find_element(By.XPATH,'//*[@id="odc.observacao"]')                                      
                        time.sleep(1)   

                        if inputText: 
                            time.sleep(1)
                            nData = "Carga "+data['numero']                                                                               
                            inputText.send_keys(nData)   
                            time.sleep(2)                                                   
                            btnSend = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[3]/div/form/div/div/div/button[1]')                                
                            if btnSend:                                    
                                # btnSend.click()
                                time.sleep(4)
                                alert = Site.findAlert(util.dir_list[i],client)
                                if alert == False:
                                    raise       
                except Exception as e:
                    raise 
                try:      
                    Site.findNumber(data['numero'],info)   
                    util.changePath(util.dir_list[i])       
                    text ="Envio completo "+data['cliente']                                      
                    Utils.writeLog(text,2)
                except Exception as e:
                    raise    
                  
            except KeyError as e:
                text ="Falha no envio"+util.dir_list[i]                                      
                Utils.writeLog(text,1)
                time.sleep(2)
                continue
                   
            except Exception as e:
                text ="Falha no envio"+util.dir_list[i]                                      
                Utils.writeLog(text,1)
                time.sleep(2)
                continue
        driver.quit()                          
        Utils.msg()    
            

    def scripRobot():
           Site.login()
           exit()
           
                  
Site.scripRobot()        

# if __name__ == "__main__":   
#     Site.scripRobot()