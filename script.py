import boto3

region_name = "us-east-1"
#profile = "prod"

elbv2 = boto3.client('elbv2')
elbv1 = boto3.client('elb')
ec2 = boto3.client('ec2')

# Get the target groups from load balancer arn
def getTargetGroups(loadBalancerArn):
    target_groups = elbv2.describe_target_groups(LoadBalancerArn = loadBalancerArn )
   
    return target_groups

# Get list of unhealthy instace under a load balancer
def getUnhealthyInstance(targetGroups):
    instances = []
    targets =''
    if(targetGroups):
        for target in targetGroups['TargetGroups']:
            targets = elbv2.describe_target_health(TargetGroupArn=target['TargetGroupArn'])
            for target in targets['TargetHealthDescriptions']:
                if target['TargetHealth']['State'] != 'healthy':
                    print ("Unhealthy Instance: ", target['Target']['Id'], " Reason: " + target['TargetHealth']['Reason'] )
        print("="*6)        
           
# Lambda entry point
def lambda_handler(event, context):
    print("Application Load Balancers")

    lbs = elbv2.describe_load_balancers(PageSize=400)
   
    # For Application load balancers
    for lb in lbs["LoadBalancers"]:
        print("\n"*2)
        print ("-"*6)
        print("Name:",lb["LoadBalancerName"])
        print("State:",lb["State"]['Code'])

        print("Instance Info:")
        print(getUnhealthyInstance(getTargetGroups(lb['LoadBalancerArn'])))
   
    print("Classic Load Balancers")    
    elbs = elbv1.describe_load_balancers(PageSize=400)
   
    # For classic load balancers
    for elb in elbs["LoadBalancerDescriptions"]:
        print("\n"*2)
        print ("-"*6)
        print("Name:",lb["LoadBalancerName"])
        instances = describe_instance_health(LoadBalancerName = lb["LoadBalancerName"])
        for instance in instances["InstanceStates"]:
            if(instance["State"] != 'InService'):
                print ("Unhealthy Instance: ", instance['InstanceId'], " Reason: " + instance['ReasonCode'])
