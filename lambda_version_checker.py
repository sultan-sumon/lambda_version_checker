import boto3
import os
def lambda_handler(event,context):
    #uses CLI command
    stream = os.popen("aws lambda list-functions --region us-east-1 --query Functions[].FunctionName --output text")
    my_dict = stream.read()
    list = my_dict.split();
    output_list = []
    
    print('Processing...')
    client = boto3.client('lambda', region_name='us-east-1')
    for x in list:
    
        response = client.get_function(
            FunctionName=x)
    
        try:
            for i in (response['Tags']):
                if response['Tags']['TEST.Code'] == "NOTUPTODATE":
                    for q in (response['Configuration']):
                        if response['Configuration']['Runtime'] == 'python2.7':
                            print(response['Configuration']['FunctionName'] + " is in " + response['Configuration'][
                                'Runtime'])
                            output = response['Configuration']['FunctionName']
                            output_list.append(output)
    
                            break;
    
                break;
    
        except:
            pass
    
    sns_client = boto3.client('sns')
    str1 = ', '.join(output_list)
    
    response = sns_client.publish(
        Message='The following lambdas are out of date: ' + str1,
        TopicArn="#########################", #ARN value can be obtained when creating SNS topic
        Subject='Out of date lambda functions'
    
    )
    
    return('Success')

